@; TODO: build tailwind css in deployment
@; TODO: add a standard nav header

@(struct header-link (name target))
@(define header-entries
	(list
		(header-link "About Me" "about_me.html")
		(header-link "Resume" "resume.html")
		(header-link "Github" "https://github.com/Kxnr")
	)
)

@(define (outlined content) 
	@; TODO: pass in additional classes
	@; TODO: pass in border width
	@; TODO: pass in background color
	(div #:class "bg-marble m-10"
		(div #:class "bg-charcoal bg-clip-padding p-4 border-l-4 border-transparent border-solid"
			content
		)
	)
)

@(define (knockout content)
	@; TODO: pass in additional classes
	(div #:class "bg-marble bg-clip-text text-transparent"
		content
	)
)

@; TODO: cards and card grid


<!DOCTYPE html>
@(->html 
	(html
		(head 
			(meta #:charset "UTF-8") 
			(title "Connor Keane Test")
			(link #:rel "stylesheet" #:type "text/css" #:media "all" #:href "css/output.css")
		)
		(body #:class "bg-charcoal text-bone border-bone z-0"
			(header #:class "sticky top-0 w-full bg-copper shadow-sm content-center items-center border-b z-10"
				@; TODO: use knockout for bottom border
				(div #:class "relative flex px-4 py-2 items-center"
					(div #:class "flex-none" "KXNR")
					(apply ol #:class "flex space-x-8 ml-auto"
						(map
							(lambda (link-struct) (li (a #:href (header-link-target link-struct) (header-link-name link-struct))))
							header-entries
						)
					)
				)
			)
			(div #:class "text-center bg-marble p-4 border-b"
				@; TODO: need something to set this apart
				(div #:class "bg-charcoal border-2"
					(div #:class "text-8xl text-transparent bg-marble bg-clip-text"
						"Connor Keane"
					)
					(div #:class "text-2xl text-transparent bg-marble bg-clip-text"
						"Developer, tinkerer, science enthusiast"
					)
				)
			)
			(div #:class "bg-charcoal relative w-full z-0"
				(div #:class "container mx-auto"
					(outlined 
						(div
							(div #:class "text-4xl" "Some Title")
							"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
						)
					)

					(outlined
						(div "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
						)
					)

					(outlined 
						(div "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
						)
					)
				)
			)
		)
		@; TODO: copyright note
	)
)
