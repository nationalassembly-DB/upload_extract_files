"""
폴더를 순회하면서 파일을 찾고 파일명을 변경하고 폴더를 생성합니다.
"""


import os
import shutil
import traceback
import pandas as pd
from natsort import natsorted


from module.create_excel.create_excel import create_excel
from module.merge_excel.compare_excel import add_attach_list, compare_excel
from module.utils.load_excel import load_excel
from module.__process__.process_log import create_log


def take_exception(e):
    """exception 발생시 출력"""
    print(f"\n!!!!!{e}!!!!!\n")
    print("-"*10)
    traceback.print_exc()
    print("-"*10)
    print("")


def process_create(input_path, excel_path):
    """#1. BOOK_ID, SEQNO가 매겨진 엑셀파일을 생성합니다"""
    try:
        create_excel(input_path, excel_path)
        print("\n=> 엑셀 파일이 정상적으로 생성되었습니다\n")
    except Exception as e:  # pylint: disable=W0718
        take_exception(e)
        if os.path.exists(excel_path):
            os.remove(excel_path)


def process_merge(base_excel_path, attach_excel_path):
    """#2. 1번에서 제작한 엑셀파일과 별도제출자료를 정리한 엑셀파일을 병합합니다"""
    try:
        while True:
            file_id = input("FILE_NAME에 들어갈 시작번호를 입력하세요 (seqNO순)\n=> ")
            try:
                int(file_id)
                break
            except ValueError:
                print("\n====숫자만 입력해주세요====\n")

        compare_excel(load_excel(base_excel_path), load_excel(
            attach_excel_path)).save(base_excel_path)
        print("\n====PDF상 답변 병합 완료. FILE_NAME병합 시작.====\n")
        add_attach_list(load_excel(base_excel_path), load_excel(
            attach_excel_path), file_id).save(base_excel_path)
        print("\n=> 엑셀 파일이 정상적으로 병합되었습니다\n")
    except Exception as e:  # pylint: disable=W0718
        take_exception(e)


def process_rename(input_path, output_path, excel_path):
    """#3. 폴더를 순회하면서 엑셀 파일 내부 파일명을 변경하고 새로운 폴더로 이동합니다."""
    df = pd.read_excel(excel_path, engine='openpyxl')

    if not all(col in df.columns for col in ['실제 파일명', 'FILE_NAME', 'FILE_PATH']):
        print("엑셀 읽기 오류! : 엑셀 파일에 필요한 열이 없습니다.")
        return

    df['FILE_PATH'] = df['FILE_PATH'].astype(str)

    for root, _, files in os.walk(input_path):
        for file in natsorted(files):
            matching_row = df[df['실제 파일명'] == file]

            if matching_row.empty:
                create_log(os.path.join(root, file))
                continue

            for index, row in matching_row.iterrows():
                actual_file_path = os.path.join(root, file)

                file_path_row = f"/inspection/reqdoc/2023/{row['BOOK_ID']}/" + \
                    f"{row['FILE_NAME']}"
                real_file_path = os.path.join(
                    "inspection", "reqdoc", "2023", str(row['BOOK_ID']), str(row['FILE_NAME']))
                target_file_path = os.path.join(output_path, real_file_path)

                target_folder = os.path.dirname(target_file_path)
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                if os.path.exists(actual_file_path):
                    shutil.copy(actual_file_path, target_file_path)

                df.at[index, 'FILE_PATH'] = file_path_row
                df.at[index, 'FILE_NAME'] = row['FILE_NAME']

    print("\n~~~엑셀 파일 수정중입니다~~~")

    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
    except PermissionError:
        print("엑셀 수정 실패! : 엑셀 파일이 열려있는 경우, 닫고 다시 실행하세요")
        return


def process_folder(input_num) -> bool:
    """전달받은 input_num을 토대로 알맞은 함수로 반환합니다."""
    if input_num in ['1', '3']:
        input_path = input("입력 폴더의 경로를 입력하세요\n=> ")
        input_path = os.path.join('\\\\?\\', input_path)

        if not os.path.isdir(input_path):
            print("\n====입력 폴더의 경로를 다시 한 번 확인하세요====\n")
            return False

    match input_num:
        case '1':
            while True:
                create_excel_path = input("엑셀 파일을 저장할 경로를 입력하세요\n=> ")
                if not create_excel_path.lower().endswith('.xlsx'):
                    print("====엑셀 파일 확장자를 입력했는지 확인해주세요====")
                process_create(input_path, create_excel_path)
                break
        case '2':
            while True:
                base_excel_path = input("1번에서 실행한 결과의 엑셀파일 경로를 입력하세요\n=> ")
                attach_excel_path = input("별도제출자료를 정리한 엑셀파일 경로를 입력하세요\n=> ")
                if os.path.exists(base_excel_path) and os.path.exists(attach_excel_path):
                    process_merge(base_excel_path, attach_excel_path)
                    break
                print("\n=> 엑셀 파일 경로를 한번 더 확인해주세요")
        case '3':
            rename_output_path = input(
                "경로 및 이름을 변경한 파일을 복사할 폴더 경로를 입력하세요\n=> ")
            rename_excel_path = input(
                "엑셀 파일의 경로를 입력하세요 (엑셀이 종료되었는지 확인하세요)\n=> ")
            process_rename(input_path, rename_output_path, rename_excel_path)

    return True
