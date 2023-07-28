var FETCH_VIDEO = false;
var FETCH_IMAGE = true;

(function requireScript() {
    const ZIPJSscriptTag = document.createElement("script");
    ZIPJSscriptTag.src =
        "https://cdn.bootcdn.net/ajax/libs/jszip/3.10.1/jszip.min.js";
    const FSAVEScriptTag = document.createElement("script");
    FSAVEScriptTag.src = 'https://cdn.bootcdn.net/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js'
    document.head.appendChild(ZIPJSscriptTag);
    document.head.appendChild(FSAVEScriptTag);
})();

var zip = null;

(function getJSZIP() {
    const timer = setInterval(() => {
        if (!zip) {
            if (window.JSZip) {
                zip = new JSZip();
                clearInterval(timer);
            }
        }
    });
})();
var userId = null;
var chunk_index = 0;

async function chunkCheckAndDownload(){
    if(Object.keys(zip.files).length > 20){
        await zipSave()
        zip = new JSZip();
        chunk_index++;
    }
}

// 滚动到最底部以加载所有
(function scrollToBottom() {
    function smoothscroll() {
        const clientHeight = document.documentElement.clientHeight; // 浏览器高度
        const scrollHeight = document.documentElement.scrollHeight; // 总高度
        const currentScroll =
            document.documentElement.scrollTop || document.body.scrollTop; // 已经被卷掉的高度
        if (scrollHeight - 10 > currentScroll + clientHeight) {
            window.requestAnimationFrame(smoothscroll);
            window.scrollTo(
                0,
                currentScroll +
                    (scrollHeight - currentScroll - clientHeight) / 2
            );
        }
    }
    return new Promise((reslove, reject) => {
        try {
            smoothscroll();
            const timer = setInterval(() => {
                const clientHeight = document.documentElement.clientHeight; // 浏览器高度
                const scrollHeight = document.documentElement.scrollHeight; // 总高度
                const currentScroll =
                    document.documentElement.scrollTop ||
                    document.body.scrollTop;
                if (clientHeight + currentScroll + 100 >= scrollHeight) {
                    setTimeout(() => {
                        clearTimeout(timer);
                    }, 1);
                    reslove();
                }
            }, 200);
        } catch (err) {
            console.log('无法滚动到底部');
            reslove();
        }
    });
})();

// 解析Note
function parseNotes() {
    return new Promise(async (resolve, reject) => {
        const notes = window.__INITIAL_STATE__.user.notes.value[0];
        try {
            index_ = 1
            for (let node of notes) {
                const { title, type, imageList, video, user } =
                    node["noteCard"];
                !userId && (userId = user.userId);
                console.log(`正在下载 === ${index_} / ${notes.length}`);
                try {
                    if (type === "video" && FETCH_VIDEO) {
                        const { consumer, media } = video;
                        const { videoId } = media;
                        const { originVideoKey } = consumer;
                        await downloadUrlFile(
                            `https://sns-video-bd.xhscdn.com/${originVideoKey}`,
                            `${index_}-${title}`,
                            videoId,
                            "mp4"
                        );
                        console.log(`视频下载完成：title:${title}`);
                    } else if (type === "normal" && FETCH_IMAGE) {
                        for (let image of imageList) {
                            const { traceId } = image;
                            await downloadUrlFile(
                                `https://sns-img-bd.xhscdn.com/${traceId}`,
                                `${index_}-${title}`,
                                traceId,
                                "png"
                            );
                            console.log(
                                `图片下载完成：title:${title}, ${traceId}`
                            );
                        }
                    }
                } catch (ex) {
                    console.log(`title=${title}下载失败,${ex}`);
                    continue;
                }
                index_ ++;
                await chunkCheckAndDownload()
            }
            resolve();
        } catch (err) {
            console.log('note解析失败');
            reject(err);
        }
    });
}

function downloadUrlFile(url, noteId, fileId, type) {
    return new Promise((resolve, reject) => {
        try {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", url, true);
            xhr.responseType = "blob";
            xhr.onload = () => {
                if (xhr.status === 200) {
                    folder = zip.folder(noteId);
                    folder.file(`${fileId}.${type}`, xhr.response);
                    resolve();
                } else {
                    throw new Error("fail");
                }
            };
            xhr.onerror = (err) => {
                console.error(`title=${noteId}下载失败,${err}`);
                resolve();
            }
            xhr.send();
        } catch (err) {
            console.log(`title=${noteId}下载失败,${err}`);
            resolve();
        }
    });
}

function waitJS() {
    return new Promise((resolve, reject) => {
        const timer = setInterval(() => {
            if (window.JSZip && window.saveAs) {
                setTimeout(() => {
                    clearTimeout(timer)
                },1)
                resolve();
            }
        });
    });
}

function zipSave(){
    return new Promise((resolve, reject) => {
        zip.generateAsync({type:"blob"}).then(function (content) {
            saveAs(content, `${userId ? `${userId}-${chunk_index}`:`result-${chunk_index}`}.zip`);
            resolve()
        });
    })
}

waitJS().then(() => {
    parseNotes().then(() => {
        console.log("下载完成，生成打包文件");
        zipSave()
    });
});
