function notice_complete(){
    const notice = document.getElementById('loadCompleteNotice');
    notice.style.display = 'block';

    setTimeout(() => {
        notice.style.display = 'none';
    }, 3000);
};
