# 가계부 관리

## 사용 기술 및 tools
> - Back-End :  Python3.8, Django3.2, MySQL 
> - ETC : Git, Github, Postman

## 모델링
<img width="739" alt="Screen Shot 2022-01-19 at 7 17 51 PM" src="https://user-images.githubusercontent.com/8315252/150111148-c982a787-8522-40c0-861c-465ba809f8f4.png">

## API

[POSTMAN API 문서](https://documenter.getpostman.com/view/16843815/UVXnFYtG)

## 설치 및 실행방법

### 배포용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/lunayyko/budgety.git
    cd budgety
    ```

2. manage.py가 있는 디렉토리 상에 아래의 내용이 포함된 my_settings.py파일을 추가한다.
    ```python
    SECRET_KEY = '랜덤한 특정 문자열'
    DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'payhere_deploy_db',
            'USER': 'myuser',
            'PASSWORD': 'mypass',
            'HOST': 'host.docker.internal',
            'PORT': '3306',
            'OPTIONS'  :  {
                'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'"
            },
        }
    }

    ALGORITHM = 'HS256'
    ```

3. docker-compose를 통해서 db와 서버를 실행시킨다. 
    ```bash
    docker-compose up
    ```

docker-compose.yml 파일에서 api 컨테이너와 mysql 컨테이너의 포트번호를 연결시키는 부분이 잘못 되었는지 에러가 나서 도커가 잘 작동하지 않는다.

### Local 개발 세팅 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/lunayyko/budgety.git
    cd budgety
    ```

2. manage.py가 있는 디렉토리 상에 아래의 내용이 포함된 my_settings.py파일을 추가한다.
    ```python
    SECRET_KEY = '랜덤한 특정 문자열'
    DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'payhere',
            'USER': 'root',
            'PASSWORD': '1234',
            'HOST': '127.0.0.1',
            'PORT': '8000',
        }
    }
    ALGORITHM = 'HS256'
    ```

3. 데이터베이스를 생성한다
    ```bash
    mysql.server start
    mysql -u root -p
    ```
    ```sql
    mysql > create database payhere character set utf8mb4 collate utf8mb4_general_ci;
    ```
4. 가상환경을 만들고 실행한다(미니콘다 설치 필요)
    ```bash
    conda create -n payhere python=3.8
    conda activate payhere
    ```

4. 라이브러리들을 설치한다
    ```python
    pip install -r requirements.txt 
    ```

5. 서버를 실행한다(파이썬이 설치 필요)
    ```python
    python manage.py runserver
    ```

## 구현 기능
### 회원가입, 로그인
- 회원가입시 password 같은 민감정보는 단방향 해쉬 알고리즘인 `bcrypt`를 이용해서 암호화 하여 database에 저장했다.
- 로그인이 성공적으로 완료되면, user정보를 토큰으로 반환할때, 양방향 해쉬 알고리즘인 `JWT`를 사용해서 응답했다.

### 가계부 작성하기
- 가계부 작성은 로그인 후에(header에 token이 있는 상태) 가능하다.
- 금액을 입력할 때 메모는 작성해도 되고 하지 않아도 된다.
- timestamp model을 사용하여 가계부 기록 시간과 업데이트 시간을 기록했다.

### 가계부 조회하기
- 로그인 후 가계부 전체 리스트, 개별 건, 삭제내역이 포함된 리스트를 조회 할 수 있다.
- 전체 리스트 조회 시에는 삭제되지 않는 내역들이 계산된 총 금액이 함께 표시된다. 

### 가계부 수정, 삭제, 복구하기
- 로그인 후 아이디(book_id)를 이용해 개별적으로 수정, 삭제 및 복구할 수 있다.
- softdelete model을 사용하여 삭제와 복구를 구현했다.