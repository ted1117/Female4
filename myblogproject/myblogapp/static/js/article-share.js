let postUrl = window.location.href;
Kakao.init("8f7bd7a4d2f7d78d444873753b489269");

function openModal() {
    document.getElementById("myModal").style.display = "block";
    document.getElementById("share-link").value = postUrl;
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

function shareTwitter() {
    // 트위터 공유 URL 설정
    const shareUrl = `https://twitter.com/intent/tweet?url=${postUrl}&text=공유할 텍스트`;
    window.open(shareUrl, "_blank");
    closeModal();
}

function shareFacebook() {
    // 페이스북 공유 URL 설정
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${postUrl}`;
    window.open(shareUrl, "_blank");
    closeModal();
}

function copyToClipboard() {
    // 클립보드에 URL 복사
    let tempInput = document.createElement("input");
    document.body.appendChild(tempInput);
    tempInput.value = postUrl;
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    // 알림 표시
    alert("포스트 링크가 클립보드에 복사되었습니다");
    closeModal();
}

function shareKakao() {
    Kakao.Link.sendScrap({
        requestUrl: postUrl,
        templateId: 98566,
        templateArgs: {
            TITLE: title,
            DESC: content,
        },
    });
    closeModal();
}