<?php
/**
 * Hackforge Machine: 78b660292cafec9a
 * Vulnerability: Basic Path Traversal
 * Theme: Minimal Nordic
 * Difficulty: 2/5
 */
?>
<!DOCTYPE html>
<html>
<head>
    <title>Basic Path Traversal Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">
    <style>

body {
    font-family: 'Source Sans Pro', sans-serif;
    background: #eceff4;
    color: #2e3440;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
}

.container {
    max-width: 700px;
    margin: 80px auto;
    background: #fff;
    padding: 50px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

h1 {
    color: #2e3440;
    font-weight: 600;
    font-size: 32px;
    margin-top: 0;
    margin-bottom: 30px;
}

p {
    color: #4c566a;
    line-height: 1.6;
}

input {
    background: #f9f9f9;
    border: 2px solid #d8dee9;
    color: #2e3440;
    padding: 15px;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
    font-size: 16px;
    font-family: 'Source Sans Pro', sans-serif;
    transition: all 0.3s;
}

input:focus {
    border-color: #5e81ac;
    outline: none;
    background: #fff;
}

button {
    background: #5e81ac;
    color: #fff;
    border: none;
    padding: 15px 35px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;
    font-size: 16px;
    font-family: 'Source Sans Pro', sans-serif;
    transition: all 0.3s;
}

button:hover {
    background: #81a1c1;
}

.result {
    margin-top: 30px;
    padding: 20px;
    background: #e5e9f0;
    border-radius: 4px;
}

.hint {
    margin-top: 20px;
    padding: 15px;
    background: #ebcb8b20;
    border-left: 4px solid #ebcb8b;
    border-radius: 4px;
}

    </style>
</head>
<body>
    <div class="container">
        <h1>Basic Path Traversal</h1>
        <p>Context: file_viewer</p>

        <form method="GET">
            <input type="text" name="input" placeholder="Search here...">
            <button type="submit">Search</button>
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