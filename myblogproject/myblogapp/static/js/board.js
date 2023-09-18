document.addEventListener('DOMContentLoaded', function () {
    // post 클래스를 가진 모든 요소를 가져옴
    const postElements = document.querySelectorAll('.post');

    // 각 요소에 클릭 이벤트 리스너를 추가
    postElements.forEach(function (post) {
        post.addEventListener('click', function () {
            // 클릭한 요소의 ID 값을 가져옴
            const postId = this.getAttribute('id');

            // ID 값을 기반으로 페이지 이동 (예: 해당 포스트의 URL)
            window.location.href = '/post?id=' + postId; // 적절한 URL로 변경
        });
    });
});