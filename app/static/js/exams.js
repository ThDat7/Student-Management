function updateExams() {
    let exams = Array.from(document.querySelectorAll('.exam'))
        .map(
            (e) => {
                let normal_exams = Array.from(e.querySelectorAll('.normal-exam'))
                    .map(
                        (e) => ({'id': parseInt(e.id), 'score': parseFloat(e.value)})
                    )
                let finalExams = Array.from(e.querySelectorAll('.final-exam'))
                    .map(
                        (e) => ({'exam_id': parseInt(e.id), 'score': parseFloat(e.value)})
                    )
                return {'id': parseInt(e.id), normal_exams, finalExams}
            }
        )

    fetch('/update', {
        method: 'POST',
        body: JSON.stringify({
            "id": 1,
            "exams": exams,
            'csrf_token': document.querySelector('input[name=csrf_token]')
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        return res.json()
    }).then(function (data) {
        console.log(data)
    });
}