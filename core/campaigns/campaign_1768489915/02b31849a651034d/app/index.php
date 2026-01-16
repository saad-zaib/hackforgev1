<?php
/**
 * Hackforge Machine: 02b31849a651034d
 * Vulnerability: Reflected XSS
 * Theme: Modern Glassmorphism
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Reflected XSS Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
}

h1 {
    color: #fff;
    margin-top: 0;
    font-weight: 600;
    font-size: 32px;
}

p {
    color: rgba(255, 255, 255, 0.9);
}

input {
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #fff;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Inter', sans-serif;
}

input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

input:focus {
    outline: none;
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.5);
}

button {
    background: rgba(255, 255, 255, 0.9);
    color: #667eea;
    border: none;
    padding: 15px 40px;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    transition: all 0.3s;
}

button:hover {
    background: #fff;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.1);
    border-left: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 5px;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Reflected XSS</h1>
        <p>Context: user_profile</p>

        <form method="GET">
            <input type="text" name="input" placeholder="What are you looking for?">
            <button type="submit">Search</button>
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
            <strong>💡 Hint:</strong> This is a user_profile context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>