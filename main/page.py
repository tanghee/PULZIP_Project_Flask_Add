from main import *
from flask import Blueprint

blueprint = Blueprint("sub", __name__, url_prefix="/sub")


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


@app.route("/")
def main_page():
    page = request.args.get("page", 1, type=int)

    board = mongo.db.board
    datas = board.find({}).limit(5).sort("pubdate", -1)

    image = mongo.db.image
    slide = image.find({})

    return render_template("/index.html", datas=datas, page=page, slide=slide, category=category)


@blueprint.route('/about')
def sub_about():
    big_tit = {key: value for key, value in category[0].items()}

    return render_template("/sub_content/about.html", category=category, big_tit=big_tit)


@blueprint.route('/location')
def sub_location():
    big_tit = {key: value for key, value in category[0].items()}

    return render_template("/sub_content/location.html", category=category, big_tit=big_tit)


@blueprint.route('/news')
def sub_news():
    big_tit = {key: value for key, value in category[0].items()}

    return render_template("/sub_content/news.html", category=category, big_tit=big_tit)


@blueprint.route('/logo')
def sub_logo():
    big_tit = {key: value for key, value in category[0].items()}

    return render_template("/sub_content/logo.html", category=category, big_tit=big_tit)


@blueprint.route('/relic')
def sub_relic():
    big_tit = {key: value for key, value in category[1].items()}

    return render_template("/sub_content/relic.html", category=category, big_tit=big_tit)


@blueprint.route('/expatiation_exhibition')
def sub_expatiation_exhibition():
    big_tit = {key: value for key, value in category[1].items()}

    return render_template("/sub_content/expatiation_exhibition.html", category=category, big_tit=big_tit)


@blueprint.route('/special_exhibition')
def sub_special_exhibition():
    big_tit = {key: value for key, value in category[1].items()}

    return render_template("/sub_content/special_exhibition.html", category=category, big_tit=big_tit)


@blueprint.route('/experience_exhibition')
def sub_experience_exhibition():
    big_tit = {key: value for key, value in category[1].items()}

    return render_template("/sub_content/experience_exhibition.html", category=category, big_tit=big_tit)


@blueprint.route('/info')
def sub_info():
    big_tit = {key: value for key, value in category[2].items()}

    return render_template("/sub_content/info.html", category=category, big_tit=big_tit)


@blueprint.route('/video')
def sub_video():
    big_tit = {key: value for key, value in category[2].items()}

    return render_template("/sub_content/video.html", category=category, big_tit=big_tit)


@blueprint.route('/field_study')
def sub_field_study():
    big_tit = {key: value for key, value in category[2].items()}

    return render_template("/sub_content/field_study.html", category=category, big_tit=big_tit)


@blueprint.route('/normal_study')
def sub_normal_study():
    big_tit = {key: value for key, value in category[2].items()}

    return render_template("/sub_content/normal_study.html", category=category, big_tit=big_tit)


@blueprint.route('/culture_book')
def sub_culture_book():
    big_tit = {key: value for key, value in category[3].items()}

    return render_template("/sub_content/culture_book.html", category=category, big_tit=big_tit)


@blueprint.route('/culture_basket')
def sub_culture_basket():
    big_tit = {key: value for key, value in category[3].items()}

    return render_template("/sub_content/culture_basket.html", category=category, big_tit=big_tit)


@blueprint.route('/pulzip_gallery')
def sub_pulzip_gallery():
    big_tit = {key: value for key, value in category[3].items()}

    return render_template("/sub_content/pulzip_gallery.html", category=category, big_tit=big_tit)


@blueprint.route('/notice')
def sub_notice():
    big_tit = {key: value for key, value in category[4].items()}

    return render_template("/sub_content/notice.html", category=category, big_tit=big_tit)


@blueprint.route('/free')
def sub_free():
    big_tit = {key: value for key, value in category[4].items()}

    return render_template("/sub_content/free.html", category=category, big_tit=big_tit)


@blueprint.route('/gallery')
def sub_gallery():
    big_tit = {key: value for key, value in category[4].items()}

    return render_template("/sub_content/gallery.html", category=category, big_tit=big_tit)


@blueprint.route('/reservation')
def sub_reservation():
    big_tit = {key: value for key, value in category[4].items()}

    return render_template("/sub_content/reservation.html", category=category, big_tit=big_tit)
