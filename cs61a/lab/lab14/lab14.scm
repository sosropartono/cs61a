(define (split-at lst n)
  (define (helper lst n og_n)
    (define (iterator lst n)
      (if (= n 0)
          lst
          (iterator (cdr lst) (- n 1))))
    (if (= n 0)
        (cons () lst)
        (if (< (length lst) n)
            (cons lst nil)
            (if (= n og_n)
                (cons
                 (cons (car lst) (helper (cdr lst) (- n 1) og_n))
                 (iterator lst n))
                (if (= n 1)
                    (cons (car lst) nil)
                    (cons (car lst) (helper (cdr lst) (- n 1) og_n)))))))
  (helper lst n n))

(define (compose-all funcs)
  (lambda (x)
    (if (null? funcs)
        x
        ((compose-all (cdr funcs)) ((car funcs) x)))))
