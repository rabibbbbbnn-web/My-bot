<?php
// ==================== [ CONFIGURATION ] ====================
$bot_token      = "9079854843:AAHAZP9ZDmtdamKJDw0F13bWdxS12T7x0_0";
$zenex_api_key  = "ZNX_LF178UCH2NIJDSBE0WKJ50LY";
$target_chat_id = 8771099641; 

$zenex_endpoint = "https://api.zenexnetwork.com/v1/numsuccess";

// ==================== [ FETCH ZENEX OTP ] ====================
function fetchZenexOtp($endpoint, $apiKey) {
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $endpoint,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            "mapikey: " . $apiKey,
            "Content-Type: application/json"
        ],
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_TIMEOUT => 10
    ]);
    $response = curl_exec($ch);
    $err = curl_error($ch);
    curl_close($ch);

    if ($err) {
        return null;
    }
    return json_decode($response, true);
}

// ==================== [ SEND TELEGRAM MESSAGE ] ====================
function sendTelegramMessage($botToken, $chatId, $text) {
    $url = "https://api.telegram.org/bot{$botToken}/sendMessage";
    $post_fields = [
        'chat_id' => $chatId,
        'text' => $text,
        'parse_mode' => 'HTML'
    ];
    
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query($post_fields),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false
    ]);
    curl_exec($ch);
    curl_close($ch);
}

// ==================== [ EXECUTION LOGIC ] ====================
$zenex_data = fetchZenexOtp($zenex_endpoint, $zenex_api_key);

if ($zenex_data && isset($zenex_data['data']['otps']) && !empty($zenex_data['data']['otps'])) {
    foreach ($zenex_data['data']['otps'] as $otp_item) {
        $service = $otp_item['service'] ?? 'Unknown Service';
        $number  = $otp_item['number'] ?? 'N/A';
        $otp     = $otp_item['otp'] ?? 'No Code';
        $country = $otp_item['country'] ?? 'N/A';
        
        $message = "🚨 <b>NEW OTP RECEIVED</b> 🚨\n\n";
        $message .= "🌐 <b>Service:</b> {$service}\n";
        $message .= "📱 <b>Number:</b> {$number}\n";
        $message .= "🌍 <b>Country:</b> {$country}\n";
        $message .= "🔑 <b>OTP Code:</b> <code>{$otp}</code>\n";
        
        sendTelegramMessage($bot_token, $target_chat_id, $message);
    }
}
?>
