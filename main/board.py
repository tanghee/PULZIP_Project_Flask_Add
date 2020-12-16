from main import *
from flask import Blueprint

blueprint = Blueprint("board", __name__, url_prefix="/board")


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


@blueprint.route("/list")
def board_list():
    # 페이지 값 (값이 없는 경우 기본값은 1), 리미트 값 (몇 개의 게시물을 나오게 할 것인지)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    board_sort = request.args.get("board_sort", -1, type=int)

    board = mongo.db.board

    tot_count = board.find({}).count()  # 게시물의 총 개수
    last_page_num = math.ceil(tot_count / limit)  # 마지막 페이지 수 = 전체 게시물 수 / 페이지당 게시물 수

    block_size = 5
    block_num = int((page - 1) / block_size)  # block 현재 위치
    block_start = int((block_size * block_num) + 1)  # block 시작 위치
    block_last = math.ceil(block_start + (block_size - 1))  # block 마지막 위치

    datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("pubdate", -1)

    if board_sort == 0:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("title", 1)
    elif board_sort == 1:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("title", -1)
    elif board_sort == 2:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("name", 1)
    elif board_sort == 3:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("name", -1)
    elif board_sort == 4:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("pubdate", -1)
    elif board_sort == 5:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("pubdate", 1)
    elif board_sort == 6:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("view", -1)
    elif board_sort == 7:
        datas = board.find({}).skip((page - 1) * limit).limit(limit).sort("view", 1)

    return render_template("/board/list.html", page=page, limit=limit, board_sort=board_sort, datas=datas, tot_count=tot_count, block_start=block_start, block_last=block_last, last_page_num=last_page_num, category=category)


@blueprint.route("/view/<idx>")
@login_required
def board_view(idx):
    # idx = request.args.get("idx")
    if idx is not None:
        page = request.args.get("page")
        board_sort = request.args.get("board_sort")

        board = mongo.db.board
        # data = board.find_one({"_id": ObjectId(idx)})
        data = board.find_one_and_update({"_id": ObjectId(idx)}, {"$inc": {"view": 1}}, return_document=True)

        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdate": data.get("pubdate"),
                "view": data.get("view"),
                "writer_id": data.get("writer_id", "")
            }

            return render_template("/board/view.html", result=result, page=page, board_sort=board_sort, category=category)
        return abort(404)


@blueprint.route('/write', methods=["GET", "POST"])
@login_required
def board_write():
    if request.method == "POST":
        name = request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")

        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board
        post = {
            "name": name,
            "title": title,
            "contents": contents,
            "pubdate": current_utc_time,
            "writer_id": session.get("id"),
            "view": 0,
        }

        x = board.insert_one(post)

        return redirect(url_for("board.board_view", idx=x.inserted_id))

    else:
        return render_template("/board/write.html", category=category)


@blueprint.route("/edit/<idx>", methods=["GET", "POST"])
def board_edit(idx):
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})

        if data is None:
            flash("해당 게시물이 존재하지 않습니다.")
            return redirect(url_for("board.board_list"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("/board/edit.html", data=data, category=category)
            else:
                flash("글 수정 권한이 없습니다.")
                return redirect(url_for("board.board_list"))
    else:
        title = request.form.get("title")
        contents = request.form.get("contents")

        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})

        if session.get("id") == data.get("writer_id"):
            board.update_one({"_id": ObjectId(idx)}, {
                "$set": {
                    "title": title,
                    "contents": contents,
                }
            })

            flash("수정되었습니다.")
            return redirect(url_for("board.board_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("board.board_list"))


@blueprint.route("/delete/<idx>")
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id": ObjectId(idx)})

    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id": ObjectId(idx)})
        flash("삭제되었습니다.")
    else:
        flash("삭제 권한이 없습니다.")

    return redirect(url_for("board.board_list"))
