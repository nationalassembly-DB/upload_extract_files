"""프로그램 설명"""


from time import sleep


def describe_program():
    """프로그램 설명"""
    print("\n\n-------별도제출자료 업로드 프로그램-------\n\n")
    print("1. BOOK_ID, SeqNO가 포함된 엑셀 파일 생성")
    print("PDF 파일로부터 BOOK_ID, SEQ_NO를 추출할 때 사용할 수 있습니다.")
    print("- BOOK_ID : 입력받은 숫자로부터 파일이름 오름차순으로 1씩 매겨집니다.")
    print("- SeqNo : PDF로부터 자동으로 불러와 매겨집니다. (StartNum : 1)\n")

    print("2. 생성된 엑셀 파일 질의합치기")
    print("1에서 생성된 엑셀 파일에 질의를 붙입니다.")
    print("질의를 매기는 과정은 위원회, 피감기관, 위원, 질의로 결정됩니다.")
    print("질의를 정리한 파일이 따로 필요합니다.\n")

    print("3. BOOK_ID를 토대로 파일명 변경 및 폴더 생성")
    print("BOOK_ID가 매겨진 엑셀 파일을 토대로 업로드 시스템에 알맞게 파일명 및 경로를 변경합니다.")
    print("- \"기본적으로 /inspection/reqdoc/2023/\"BOOK_ID\"/\"별도제출파일명\" 으로 경로가 생성됩니다")
    print("- 경로가 생성이 완료된 이후, 엑셀 파일의 \'경로명\'열을 생성된 경로명으로 변경됩니다.\n")

    print("3. 로그 파일 삭제")
    print("기본적으로 경로명 혹은 파일명을 토대로 파일명 변경을 시도합니다.")
    print("하지만 간혹 파일명 변경 등의 이슈로 인해 성공적으로 작업이 되지 않을 경우가 있습니다.")
    print("그럴 경우, 바탕화면에 로그파일이 생성되어 문제가 발생한 파일의 경로명을 남깁니다.")
    print("더 이상 로그 파일이 필요가 없을 경우, 로그 파일을 삭제할 수 있습니다.")

    sleep(5)