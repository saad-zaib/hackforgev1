<?php
/**
 * Hackforge Machine: 50f2114508234b0b
 * Vulnerability: Reflected XSS
 * Theme: Cyberpunk Neon
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reflected XSS Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Orbitron', monospace;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 100%);
    background-attachment: fixed;
    color: #00ff9f;
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 50px auto;
    padding: 40px;
    background: rgba(10, 10, 30, 0.9);
    border: 2px solid #ff0080;
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(255, 0, 128, 0.5), inset 0 0 20px rgba(255, 0, 128, 0.1);
}

h1 {
    color: #ff0080;
    text-shadow: 0 0 10px rgba(255, 0, 128, 0.8), 0 0 20px rgba(255, 0, 128, 0.5);
    margin-top: 0;
    font-size: 2.5em;
    text-transform: uppercase;
    letter-spacing: 3px;
}

input {
    background: #000;
    border: 2px solid #00ff9f;
    color: #00ff9f;
    padding: 15px;
    font-family: 'Orbitron', monospace;
    width: 100%;
    box-sizing: border-box;
    border-radius: 5px;
    font-size: 16px;
    box-shadow: 0 0 10px rgba(0, 255, 159, 0.3);
    transition: all 0.3s;
}

input:focus {
    outline: none;
    box-shadow: 0 0 20px rgba(0, 255, 159, 0.6);
    border-color: #ff0080;
}

button {
    background: linear-gradient(45deg, #ff0080, #ff00ff);
    border: none;
    color: #fff;
    padding: 15px 40px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase;
    border-radius: 5px;
    font-family: 'Orbitron', monospace;
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.6);
    transition: all 0.3s;
    margin-top: 15px;
}

button:hover {
    box-shadow: 0 0 30px rgba(255, 0, 255, 0.8);
    transform: translateY(-2px);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(0, 255, 159, 0.05);
    border: 1px solid #00ff9f;
    border-radius: 5px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(255, 0, 128, 0.1);
    border-left: 4px solid #ff0080;
    border-radius: 5px;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Reflected XSS</h1>
        <p>Context: message_board</p>

        <form method="GET">
            <input type="text" name="input" placeholder="Enter your query...">
            <button type="submit">Execute</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            $input = str_replace('s', '', $input);
            $input = str_replace('o', '', $input);
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a message_board context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>