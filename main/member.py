from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix="/member")


category = [
        {"박물관소개": {
            "관장 인사글": "about",
            "관람 안내 및 오시는 길": "location",
            "관련 기사": "news",
            "로고 소개": "logo",
        }},
        {"풀짚공예 전시실": {
            "소장유물 소개": "relic",
            "상설 전시": "expatiation_exhibition",
            "특별 전시": "special_exhibition",
            "체험교육 전시": "experience_exhibition",
        }},
        {"풀짚공예 교육": {
            "풀짚공예란?": "info",
            "만들기 동영상": "video",
            "체험학습": "field_study",
            "일반&전문가 심화과정": "normal_study",
        }},
        {"풀짚 문화": {
            "책 소개": "culture_book",
            "바구니여행": "culture_basket",
            "풀짚갤러리": "pulzip_gallery",
        }},
        {"커뮤니티": {
            "공지사항": "notice",
            "자유게시판": "free",
            "포토갤러리": "gallery",
            "체험예약": "reservation",
        }},
    ]


@blueprint.route('/join', methods=["GET", "POST"])
def member_join():
    if request.method == "POST":
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name == "" or email == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("/member/join.html", category=category)

        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("/member/join.html", category=category)

        members = mongo.db.members
        cnt = members.find({"email": email}).count()
        if cnt > 0:
            flash("중복된 이메일 주소입니다.")
            return render_template("/member/join.html", category=category)

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        post = {
            "name": name,
            "email": email,
            "pass": pass1,
            "join_date": current_utc_time,
            "login_time": "",
            "login_count": 0,
        }

        members.insert_one(post)
        return render_template("/member/login.html", category=category)

    else:
        return render_template("/member/join.html", category=category)


@blueprint.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        next_url = request.form.get("next_url")

        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원 정보가 없습니다.")
            return redirect(url_for("member.member_login"))
        else:
            if data.get("pass") == password:
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True

                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board.board_list"))

            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member.member_login"))
        return ""

    else:
        next_url = request.args.get("next_url", type=str)

        if next_url is not None:
            return render_template("/member/login.html", next_url=next_url, category=category)
        else:
            return render_template("/member/login.html", category=category)


@blueprint.route("/logout")
def member_logout():
    try:
        del session["name"]
        del session["id"]
        del session["email"]

    except:
        pass

    return redirect(url_for('main_screen'))
