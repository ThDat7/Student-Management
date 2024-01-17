console.log(123)
var allRow = $('.teach-detail tbody tr')

$('.search-student').on('input', function () {
    var keyword = $(this).val()

    if (keyword == '') {
        for (var i = 0; i <= allRow.length; i++) {
            $('.teach-detail tbody').append(allRow[i])
        }
        return;
    }

    if (!keyword) return;

    var row_search = []
    $.each(allRow, (i, e) => {
        var row_text = ''
        row_text += $($(e).find('td')[1]).text() + ' '
        row_text += $($(e).find('td')[2]).text()

        row_text = row_text
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/đ/g, "d")
            .replace(/Đ/g, "D");

        if (row_text.includes(keyword))
            row_search.push(e)
    })
    $('.teach-detail tbody').html('')
    if (row_search.length === 0)
        $('.teach-detail tbody').html(`Khong tim thay hoc sinh`)
    for (var i = 0; i <= row_search.length; i++) {
        $('.teach-detail tbody').append(row_search[i])
    }
})

function eventShowExamModal(event) {
    let button = $(event.relatedTarget)
    let modal = $(this)
    modal.find('input').focus()

    let exam_id = parseInt(button.closest('.exam').data('exam-id'))

    let id = parseInt(button.data('id'))
    let score = parseFloat(button.text())

    let submitBtn = modal.find('button.submit')
    let deleteBtn = modal.find('button.delete')

    submitBtn.off("click")
    deleteBtn.off("click")
    modal.find('input').val('')
    $('span.msg').text('')

    let submitHandler = () => {
    }
    if (button.parent().data('exam-type') == 'normal') {
        if (id) {
            modal.find('input').val(score)
            deleteBtn.show()
            submitHandler = ajaxUpdateNormalExam
            deleteBtn.on('click', ajaxDeleteNormalExam)
        } else {
            deleteBtn.hide()
            submitHandler = ajaxCreateNormalExam
        }
    } else if (button.parent().data('exam-type') == 'final') {
        if (score)
            modal.find('input').val(score)

        deleteBtn.hide()
        submitHandler = ajaxUpdateFinalExam
    }

    submitBtn.on('click', handleSubmit)

    function ajaxSuccess(data, method) {
        modal.modal('hide')

        if (method == 'CREATE') {
            button.before(`<button type="button" class="btn btn-secondary" data-toggle="modal"
                                data-target="#exam-modal"
                                data-id="${data.id}"
                                data-score="${data.score}">
                            ${Number.isInteger(data.score) ? data.score.toFixed(1) : data.score}
                        </button>`)

            let factor = button.data('factor');
            let btnCount = button.parent().children('button').length
            if ((factor === 'I' && btnCount >= 6) || (factor === 'II' && btnCount >= 4))
                button.remove()
        }

        if (method == 'UPDATE') {
            button.html(Number.isInteger(data.score) ? data.score.toFixed(1) : data.score)
            button.data('score', data.score)
        }

        if (method == 'DELETE') {
            let hasAddBtn = button.parent().children('button.add').length === 1
            if (!hasAddBtn) {
                let factor = button.parent().data('factor');
                button.parent().append(`
                            <button type="button" class="btn btn-success add" data-toggle="modal"
                                    data-target="#exam-modal"
                                    data-factor="${factor}">
                                Thêm
                            </button>`)
            }
            button.remove()
        }

    }

    function handleSubmit() {
        score = parseFloat(modal.find('.modal-body input').val())
        if (score >= 0 && score <= 10) {
            $('span.msg').text('')
            submitHandler()
        } else
            $('span.msg').text('Điểm không hợp lệ')
    }

    async function ajaxCreateExam() {
        let teach_id = parseInt($('table.teach-detail').data('teach-id'))
        let student_id = parseInt(button.closest('.exam').data('student-id'))

        await $.ajax({
            type: 'POST',
            url: `/api/exam`,
            data: JSON.stringify({
                'student_id': student_id,
                'teach_id': teach_id
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: (data) => {
                exam_id = data.id
                button.closest('.exam').data('exam-id', data.id)
            }
        })
    }

    async function ajaxUpdateFinalExam() {
        if (!exam_id)
            await ajaxCreateExam()

        score = parseFloat(modal.find('input').val())
        $.ajax({
            type: 'POST',
            url: `/api/final_exam/${exam_id}`,
            data: JSON.stringify({
                'score': score
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: (data) => {
                ajaxSuccess(data, 'UPDATE')
            }
        })
    }

    async function ajaxCreateNormalExam() {
        if (!exam_id)
            await ajaxCreateExam()

        score = parseFloat(modal.find('input').val())
        let factor = button.data('factor')
        $.ajax({
            type: 'POST',
            url: `/api/normal_exam`,
            data: JSON.stringify({
                'exam_id': exam_id,
                'factor': factor,
                'score': score
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: (data) => {
                ajaxSuccess(data, 'CREATE')
            }
        })

    }

    function ajaxUpdateNormalExam() {
        score = parseFloat(modal.find('input').val())
        $.ajax({
            type: 'PUT',
            url: `/api/normal_exam/${id}`,
            data: JSON.stringify({
                'exam_id': exam_id,
                'score': score
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: (data) => {
                ajaxSuccess(data, 'UPDATE')
            }
        })
    }

    function ajaxDeleteNormalExam() {
        $.ajax({
            type: 'DELETE',
            url: `/api/normal_exam/${id}`,
            data: JSON.stringify({
                'exam_id': exam_id
            }),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: (data) => {
                ajaxSuccess(data, 'DELETE')
            }
        })
    }
}


$('#exam-modal').off('show.bs.modal')
$('#exam-modal').on('show.bs.modal', eventShowExamModal)
