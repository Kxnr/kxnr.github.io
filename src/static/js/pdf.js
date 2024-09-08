class PdfDoc {
    constructor(doc) {
        this.pageNum = 1;
        this.pending = null;
        this.doc = doc;
    }

    queue(promise) {
        this.pending = promise;
        this.pending.then((value) => {
            this.pending = null;
            return value;
        });
        return this.pending;
    }

    getPage(pageNum=this.pageNum) {
        return this.queue(this.doc.getPage(pageNum))
    }

    render(canvas) {
        if(this.pending) {
            // NOTE: this won't skip rendering pages, if next
            // is pressed multiple times, then each page will
            // render in sequence
            this.pending.then(() => this.render(canvas));
        } else {
            return this.getPage().then((page) => {
                let viewport = page.getViewport({scale: 1.0});
                let scale = canvas.parent().width() / viewport.width;

                viewport = page.getViewport({scale: scale});

                // jquery resize lead to rendering issue, cause unknown
                canvas.get(0).height = viewport.height;
                canvas.get(0).width = viewport.width;

                let renderContext = {
                    canvasContext: canvas.get(0).getContext('2d'),
                    viewport: viewport,
                };
                this.queue(page.render(renderContext).promise);
            })
        }

        return this.pending;
    }

    next() {
        if (this.pageNum >= this.doc.numPages) {
            return;
        }
        this.pageNum++;
    }

    prev() {
        if (this.pageNum <= 1) {
            return;
        }
        this.pageNum--;
    }
}

// TODO: clean up this 'API,' this ends up using the self invoking
// pdf function that is defined after this
class PdfView {

    constructor(src, canvas, next=null, prev=null) {
        // canvas, next, and prev should be the result of a jquery
        // selector expression

        this.doc = null;
        this.pages = null;
        this.canvas = canvas;
        this.nextButton = next;
        this.prevButton = prev;

        pdf.load(src).then((_doc) => {
            this.doc = _doc;
            this.pages = this.doc.doc.numPages;
            this.checkControls();

            pdf.display(_doc, canvas);

            if(this.nextButton) {
                this.nextButton.click(() => this.next());
            }

            if(this.prevButton) {
                this.prevButton.click(() => this.prev());
            }
        });

        $(() => $(window).resize(() => pdf.display(this.doc, canvas)));
    }

    checkControls() {
        if(this.doc.pageNum >= this.pages) {
            this.nextButton.prop('disabled', true);
        } else {
            this.nextButton.prop('disabled', false);
        }

        if(this.doc.pageNum <= 1) {
            this.prevButton.prop('disabled', true);
        } else {
            this.prevButton.prop('disabled', false);
        }
    }

    next() {
        pdf.next(this.doc, this.canvas);
        this.checkControls();
    }

    prev() {
        pdf.prev(this.doc, this.canvas);
        this.checkControls();
    }
}

(function(pdf, $, undefined) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = "/static/js/pdfjs-dist/build/pdf.worker.js"

    pdf.load = function(url) {
        return pdfjsLib.getDocument(url).promise.then((doc) => new PdfDoc(doc));
    }

    pdf.display = function(doc, canvas) {
        return doc.render(canvas);
    }

    pdf.next = function(doc, canvas) {
        doc.next();
        pdf.display(doc, canvas);
    }

    pdf.prev = function(doc, canvas) {
        doc.prev();
        pdf.display(doc, canvas);
    }

    pdf.view = PdfView;

} (window.pdf = window.pdf || {}, jQuery));