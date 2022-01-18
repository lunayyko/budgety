FROM python:3.8
# 기반이 될 이미지
ENV PYTHONUNBUFFERED=1

WORKDIR  /usr/src/app
# 작업 디렉토리(default) 설정 : 어떤 폴더를 불러와서 작업공간으로 쓸것인지

COPY . .
# 현재 경로에 존재하는 모든 소스파일을 이미지에 복사

# COPY requirements.txt /usr/src/app
# 이미지 파일 안에 패키기 설치하기 위해서

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc

RUN pip install -r requirements.txt
#설치 정보를 불러들여서 패키지를 설치

EXPOSE 8000
# 8000번 포트를 외부에 개방하도록 설정

# CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"]
# gunicorn(manage.py runserver하는 것)을 사용해서 서버를 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "payhere.wsgi:application"]
# gunicorn을 사용해서 서버를 실행