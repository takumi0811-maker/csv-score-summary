# score_summary.py
# CSVファイルから参加者ごとのスコアを読み込み、平均点・最高点・最低点を表示するプログラム

import csv
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

# 読み込むCSVファイルの名前
CSV_FILE = "課題2.csv"
# このプログラムと同じフォルダにあるCSVファイルの場所（どこから実行しても見つかるようにする）
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), CSV_FILE)


def read_scores(file_path):
    """CSVファイルを読み込み、{名前: [スコア, スコア, ...]} の形の辞書を返す"""
    scores = {}

    try:
        # encoding="utf-8-sig" で開く（UTF-8で文字化けを防ぐ。先頭にBOMがあっても正しく読める）
        with open(file_path, encoding="utf-8-sig", newline="") as f:
            # DictReader は1行目の見出しを使って、各行を {"名前": ..., "スコア": ...} の形で読み込む
            reader = csv.DictReader(f)

            # 必要な列（名前・スコア）が見出しにあるか確認する
            if reader.fieldnames is None:
                raise ValueError("CSVファイルが空です。")
            for column in ["名前", "スコア"]:
                if column not in reader.fieldnames:
                    raise ValueError(f"見出しに「{column}」列がありません。（見出し: {reader.fieldnames}）")

            # 1行ずつ取り出して、名前ごとにスコアをリストへ追加する
            # 見出しが1行目なので、データは2行目から始まる
            for line_number, row in enumerate(reader, start=2):
                name = (row["名前"] or "").strip()
                score_text = (row["スコア"] or "").strip()

                if name == "":
                    raise ValueError(f"{line_number}行目: 名前が空です。")
                if score_text == "":
                    raise ValueError(f"{line_number}行目: スコアが空です。")

                # スコアの文字列を整数に変換する（数字でなければエラー）
                try:
                    score = int(score_text)
                except ValueError:
                    raise ValueError(f"{line_number}行目: スコア「{score_text}」が整数ではありません。")

                # 初めて出てきた名前なら空のリストを用意してから追加する
                if name not in scores:
                    scores[name] = []
                scores[name].append(score)

    except UnicodeDecodeError:
        raise ValueError("文字コードがUTF-8ではないため読み込めません。UTF-8で保存し直してください。")

    if not scores:
        raise ValueError("集計できるデータが1行もありません。")

    return scores


def round_half_up(value):
    """一般的な四捨五入で小数点第1位までにする（例: 83.65 → 83.7、83.75 → 83.8）"""
    # Pythonの round() は「偶数への丸め」なので、round(0.25, 1) が 0.3 ではなく 0.2 になる。
    # そのため Decimal の ROUND_HALF_UP（一般的な四捨五入）を使う。
    return Decimal(value).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def main():
    # ① CSVファイルを読み込む（問題があれば分かりやすいメッセージを出して終了する）
    try:
        scores = read_scores(CSV_PATH)
    except FileNotFoundError:
        print(f"エラー: 「{CSV_FILE}」が見つかりません。このプログラムと同じフォルダに置いてください。")
        sys.exit(1)
    except ValueError as e:
        print(f"エラー: データに問題があります。{e}")
        sys.exit(1)

    # ② 参加者ごとに計算して表示する
    print("【集計結果】")
    print("| 参加者名 | 平均点 | 最高点 | 最低点 |")
    print("| ---- | ---- | --- | --- |")

    for name, score_list in scores.items():
        # 平均点 = 合計 ÷ 個数（Decimalで計算して誤差を防ぎ、四捨五入する）
        average = round_half_up(Decimal(sum(score_list)) / Decimal(len(score_list)))
        highest = max(score_list)  # 最高点
        lowest = min(score_list)   # 最低点
        print(f"| {name} | {average} | {highest} | {lowest} |")


# このファイルを直接実行したときだけ main() を動かす
if __name__ == "__main__":
    main()
