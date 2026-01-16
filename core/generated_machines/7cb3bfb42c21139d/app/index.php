<?php
/**
 * Hackforge Machine: 7cb3bfb42c21139d
 * Vulnerability: Direct Command Injection
 * Theme: Dark Hacker
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Direct Command Injection Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Fira Code', monospace;
    background: #0a0a0a;
    color: #e0e0e0;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 900px;
    margin: 50px auto;
    background: #1a1a1a;
    border-radius: 15px;
    padding: 40px;
    border: 1px solid #333;
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
}

h1 {
    color: #ff7300;
    border-bottom: 2px solid #ff7300;
    padding-bottom: 10px;
    margin-top: 0;
    font-size: 28px;
}

input {
    background: #0a0a0a;
    border: 2px solid #333;
    color: #e0e0e0;
    padding: 15px;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    transition: all 0.3s;
}

input:focus {
    border-color: #ff7300;
    outline: none;
    box-shadow: 0 0 10px rgba(255, 115, 0, 0.3);
}

button {
    background: #ff7300;
    color: #000;
    border: none;
    padding: 15px 40px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    text-transform: uppercase;
    font-family: 'Fira Code', monospace;
    margin-top: 15px;
    transition: all 0.3s;
}

button:hover {
    background: #ff9500;
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(255, 115, 0, 0.4);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 115, 0, 0.05);
    border-left: 3px solid #ff7300;
    border-radius: 5px;
}

.hint {
    background: rgba(255, 115, 0, 0.1);
    border-left: 4px solid #ff7300;
    padding: 15px;
    margin-top: 20px;
    border-radius: 5px;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Direct Command Injection</h1>
        <p>Context: ping_utility</p>

        <form method="GET">
            <input type="text" name="input" placeholder="Enter search query...">
            <button type="submit">Execute</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            $input = str_replace('s', '', $input);
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a ping_utility context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>