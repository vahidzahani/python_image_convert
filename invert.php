<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['docx_file'])) {
    // دایرکتوری برای ذخیره فایل‌های آپلودشده
    $upload_dir = 'uploads/';
    if (!is_dir($upload_dir)) {
        mkdir($upload_dir, 0777, true);
    }

    // نام فایل و مسیر آن
    $file_name = basename($_FILES['docx_file']['name']);
    $upload_file = $upload_dir . $file_name;

    // انتقال فایل به دایرکتوری uploads
    if (move_uploaded_file($_FILES['docx_file']['tmp_name'], $upload_file)) {
        // اجرای اسکریپت Python
        $output_file = 'output.docx';
        $command = escapeshellcmd("python invert_doc.py $upload_file --out $output_file");
        exec($command, $output, $return_var);

        // بررسی اینکه آیا فایل خروجی تولید شده است یا نه
        if ($return_var === 0 && file_exists($output_file)) {
            // دانلود فایل خروجی
            header('Content-Description: File Transfer');
            header('Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document');
            header('Content-Disposition: attachment; filename="' . basename($output_file) . '"');
            header('Expires: 0');
            header('Cache-Control: must-revalidate');
            header('Pragma: public');
            header('Content-Length: ' . filesize($output_file));
            flush(); // Flush system output buffer
            readfile($output_file);
            exit;
        } else {
            echo "خطا در پردازش فایل. لطفاً دوباره تلاش کنید.";
        }
    } else {
        echo "خطا در آپلود فایل.";
    }
} else {
    echo "فایل آپلود نشده است.";
}
?>
