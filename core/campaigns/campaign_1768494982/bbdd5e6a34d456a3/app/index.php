<?php
/**
 * Hackforge Machine: bbdd5e6a34d456a3
 * Vulnerability: Encoded Path Traversal
 * Theme: Dark Purple
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Encoded Path Traversal Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Roboto', sans-serif;
    background: #1a1a2e;
    color: #eee;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 850px;
    margin: 60px auto;
    background: #16213e;
    border-radius: 12px;
    padding: 45px;
    border: 1px solid #9b59b6;
    box-shadow: 0 8px 40px rgba(155, 89, 182, 0.3);
}

h1 {
    color: #9b59b6;
    margin-top: 0;
    font-size: 32px;
    font-weight: 500;
}

p {
    color: #ccc;
}

input {
    background: #0f1624;
    border: 2px solid #2a2a4e;
    color: #fff;
    padding: 15px;
    border-radius: 8px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    transition: all 0.3s;
}

input:focus {
    outline: none;
    border-color: #9b59b6;
    box-shadow: 0 0 15px rgba(155, 89, 182, 0.4);
}

button {
    background: linear-gradient(135deg, #9b59b6, #8e44ad);
    color: #fff;
    border: none;
    padding: 15px 40px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    margin-top: 15px;
    transition: all 0.3s;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(155, 89, 182, 0.5);
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: rgba(155, 89, 182, 0.1);
    border-left: 3px solid #9b59b6;
    border-radius: 5px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: rgba(155, 89, 182, 0.15);
    border-left: 4px solid #9b59b6;
    border-radius: 5px;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Encoded Path Traversal</h1>
        <p>Context: file_viewer</p>

        <form method="GET">
            <input type="text" name="input" placeholder="Search...">
            <button type="submit">Submit Query</button>
        </form>

        <?php
        if (isset($_GET['input'])) {
            $input = $_GET['input'];
            $input = str_replace('d', '', $input);
            echo '<div class="result">';
            echo '<h3>Results:</h3>';
            echo '<div>' . $input . '</div>';
            echo '</div>';
        }
        ?>

        <div class="hint">
            <strong>💡 Hint:</strong> This is a file_viewer context. Can you find the vulnerability?
        </div>
    </div>
</body>
</html>