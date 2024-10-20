#lang racket/base

(require txexpr)
(provide (all-defined-out))

(module setup racket/base
  (provide (all-defined-out))
  (define command-char #\@)
)


(define (outlined . content)
	(txexpr* 'div '((class "bg-background-fade m-4"))
	  (txexpr 'div '((class "bg-charcoal bg-clip-padding p-4 border-4 border-transparent border-solid")) content)
	)
)

(define (title . content)
	(txexpr 'div '((class "text-4xl border-b w-full border-bone text-bone mb-2")) content)
)

(define (page-title . content)
  (txexpr 'title empty content)
)

(define (break)
  (txexpr 'br empty empty)
)
