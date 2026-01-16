<?php
/**
 * Hackforge Machine: 3d5f9d164747f455
 * Vulnerability: Encoded Path Traversal
 * Theme: Retro Terminal
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Encoded Path Traversal Challenge</title>
    
    <style>

body {
    font-family: 'Courier New', monospace;
    background: #000;
    color: #00ff00;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background: #001100;
    border: 3px solid #00ff00;
    font-size: 14px;
    box-shadow: inset 0 0 50px rgba(0, 255, 0, 0.1);
}

.terminal-header {
    background: #003300;
    padding: 10px;
    margin: -20px -20px 20px -20px;
    border-bottom: 2px solid #00ff00;
    font-weight: bold;
    text-transform: uppercase;
}

h1 {
    color: #00ff00;
    margin-top: 0;
    font-size: 24px;
    font-weight: normal;
}

.prompt::before {
    content: "root@hackforge:~$ ";
    color: #33ff33;
    font-weight: bold;
}

input {
    background: #000;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 10px;
    font-family: 'Courier New', monospace;
    width: 100%;
    box-sizing: border-box;
    font-size: 14px;
}

input:focus {
    outline: none;
    background: #001100;
}

button {
    background: #003300;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 10px 30px;
    cursor: pointer;
    font-family: 'Courier New', monospace;
    margin-top: 10px;
    text-transform: uppercase;
}

button:hover {
    background: #00ff00;
    color: #000;
}

.result {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
}

.hint {
    margin-top: 20px;
    padding: 10px;
    border-left: 3px solid #00ff00;
    background: rgba(0, 255, 0, 0.05);
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Encoded Path Traversal</h1>
        <p>Context: file_viewer</p>

        <form method="GET">
            <input type="text" name="input" placeholder="_">
            <button type="submit">[EXECUTE]</button>
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