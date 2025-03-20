/*
Plugin Name: Luxe Horizons Chatbot
Plugin URI: https://luxehorizons.com
Description: A WordPress chatbot plugin powered by Gemini AI to assist users with travel inquiries.
Version: 1.0
Author: Luxe Horizons
Author URI: https://luxehorizons.com
License: GPL2
*/

// Enqueue chatbot styles and scripts
function luxe_chatbot_enqueue_scripts() {
    wp_enqueue_style('luxe-chatbot-style', plugin_dir_url(__FILE__) . 'css/chatbot.css');
    wp_enqueue_script('luxe-chatbot-script', plugin_dir_url(__FILE__) . 'js/chatbot.js', array('jquery'), null, true);
    wp_localize_script('luxe-chatbot-script', 'chatbot_ajax', array('ajaxurl' => admin_url('admin-ajax.php')));
}
add_action('wp_enqueue_scripts', 'luxe_chatbot_enqueue_scripts');

// Chatbot HTML structure
function luxe_chatbot_display() {
    echo '<div id="luxe-chatbot">
            <div id="chatbot-header">Luxe Horizons Chat</div>
            <div id="chatbot-messages"></div>
            <input type="text" id="chatbot-input" placeholder="Ask me about travel..." />
            <button id="chatbot-send">Send</button>
          </div>';
}
add_action('wp_footer', 'luxe_chatbot_display');

// Handle chatbot AJAX request
function luxe_chatbot_handle_request() {
    if (!isset($_POST['message']) || empty($_POST['message'])) {
        wp_send_json_error(['error' => 'Message is required']);
    }
    
    $user_message = sanitize_text_field($_POST['message']);
    $api_url = 'https://chatbot-ai-9vfs.onrender.com/chat';
    $response = wp_remote_post($api_url, array(
        'body'    => json_encode(['message' => $user_message]),
        'headers' => array('Content-Type' => 'application/json'),
        'method'  => 'POST',
    ));
    
    if (is_wp_error($response)) {
        wp_send_json_error(['error' => 'Failed to connect to chatbot']);
    }
    
    $response_body = wp_remote_retrieve_body($response);
    wp_send_json_success(json_decode($response_body, true));
}
add_action('wp_ajax_luxe_chatbot_request', 'luxe_chatbot_handle_request');
add_action('wp_ajax_nopriv_luxe_chatbot_request', 'luxe_chatbot_handle_request');
