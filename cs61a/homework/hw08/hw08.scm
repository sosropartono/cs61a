(define (my-filter func lst)
  (if (null? lst)
      nil
      (if (func (car lst))
          (cons (car lst) (my-filter func (cdr lst)))
          (my-filter func (cdr lst)))))

(define (interleave s1 s2)
  (if (null? s1)
      s2
      (if (null? s2)
          s1
          (cons (car s1)
                (cons (car s2) (interleave (cdr s1) (cdr s2)))))))

(define (accumulate merger start n term)
  (if (= n 1)
      (merger start (term n))
      (merger (term n)
              (accumulate merger start (- n 1) term))))

(define (length lst)
  (if (null? lst)
      0
      (+ 1 (length (cdr lst)))))

(define (finder lst element)
  (if (null? lst)
      #f
      (if (= element (car lst))
          #t
          (finder (cdr lst) element))))

(define (no-repeats lst)
  (if (null? lst)
      nil
      (if (not (finder (cdr lst) (car lst)))
          (cons (car lst) (no-repeats (cdr lst)))
          (no-repeats (cdr lst)))))
