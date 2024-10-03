# Outlookで新規メールを受信したらその件名をコンソール画面に出力するスクリプト
# 処理の条件：Outlookを立ち上げている必要がある（そもそも立ち上げていないとメール受信できない)
import win32com.client
import win32timezone 
import time

def on_new_mail(item):
    if item.Class == 43:  # 43はMailItemのクラス
        print(f"新しいメールを受信しました: {item.Subject}")

def main():
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)  # 6は受信トレイ

    # 受信トレイのアイテムを監視
    inbox_items = inbox.Items
    inbox_items.Sort("[ReceivedTime]", True)

    # 受信トレイの最新メールを取得
    latest_item = inbox_items.GetFirst()
    latest_time = latest_item.ReceivedTime if latest_item else None

    while True:
        time.sleep(5)  # 5秒間隔でチェック
        
        # 最新のメールを取得
        inbox_items = inbox.Items
        inbox_items.Sort("[ReceivedTime]", True)
        current_item = inbox_items.GetFirst()

        if current_item and (latest_time is None or current_item.ReceivedTime != latest_time):
            latest_time = current_item.ReceivedTime
            on_new_mail(current_item)
        

if __name__ == "__main__":
    main()
