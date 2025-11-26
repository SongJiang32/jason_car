;; Auto-generated. Do not edit!


(when (boundp 'bluesea2::Control)
  (if (not (find-package "BLUESEA2"))
    (make-package "BLUESEA2"))
  (shadow 'Control (find-package "BLUESEA2")))
(unless (find-package "BLUESEA2::CONTROL")
  (make-package "BLUESEA2::CONTROL"))
(unless (find-package "BLUESEA2::CONTROLREQUEST")
  (make-package "BLUESEA2::CONTROLREQUEST"))
(unless (find-package "BLUESEA2::CONTROLRESPONSE")
  (make-package "BLUESEA2::CONTROLRESPONSE"))

(in-package "ROS")





(defclass bluesea2::ControlRequest
  :super ros::object
  :slots (_topic _func _flag _params ))

(defmethod bluesea2::ControlRequest
  (:init
   (&key
    ((:topic __topic) "")
    ((:func __func) "")
    ((:flag __flag) 0)
    ((:params __params) "")
    )
   (send-super :init)
   (setq _topic (string __topic))
   (setq _func (string __func))
   (setq _flag (round __flag))
   (setq _params (string __params))
   self)
  (:topic
   (&optional __topic)
   (if __topic (setq _topic __topic)) _topic)
  (:func
   (&optional __func)
   (if __func (setq _func __func)) _func)
  (:flag
   (&optional __flag)
   (if __flag (setq _flag __flag)) _flag)
  (:params
   (&optional __params)
   (if __params (setq _params __params)) _params)
  (:serialization-length
   ()
   (+
    ;; string _topic
    4 (length _topic)
    ;; string _func
    4 (length _func)
    ;; int8 _flag
    1
    ;; string _params
    4 (length _params)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _topic
       (write-long (length _topic) s) (princ _topic s)
     ;; string _func
       (write-long (length _func) s) (princ _func s)
     ;; int8 _flag
       (write-byte _flag s)
     ;; string _params
       (write-long (length _params) s) (princ _params s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _topic
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _topic (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _func
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _func (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; int8 _flag
     (setq _flag (sys::peek buf ptr- :char)) (incf ptr- 1)
     (if (> _flag 127) (setq _flag (- _flag 256)))
   ;; string _params
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _params (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass bluesea2::ControlResponse
  :super ros::object
  :slots (_code _value ))

(defmethod bluesea2::ControlResponse
  (:init
   (&key
    ((:code __code) 0)
    ((:value __value) "")
    )
   (send-super :init)
   (setq _code (round __code))
   (setq _value (string __value))
   self)
  (:code
   (&optional __code)
   (if __code (setq _code __code)) _code)
  (:value
   (&optional __value)
   (if __value (setq _value __value)) _value)
  (:serialization-length
   ()
   (+
    ;; int32 _code
    4
    ;; string _value
    4 (length _value)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _code
       (write-long _code s)
     ;; string _value
       (write-long (length _value) s) (princ _value s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _code
     (setq _code (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; string _value
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _value (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass bluesea2::Control
  :super ros::object
  :slots ())

(setf (get bluesea2::Control :md5sum-) "806ff7bf5db5481c099a10480669f74f")
(setf (get bluesea2::Control :datatype-) "bluesea2/Control")
(setf (get bluesea2::Control :request) bluesea2::ControlRequest)
(setf (get bluesea2::Control :response) bluesea2::ControlResponse)

(defmethod bluesea2::ControlRequest
  (:response () (instance bluesea2::ControlResponse :init)))

(setf (get bluesea2::ControlRequest :md5sum-) "806ff7bf5db5481c099a10480669f74f")
(setf (get bluesea2::ControlRequest :datatype-) "bluesea2/ControlRequest")
(setf (get bluesea2::ControlRequest :definition-)
      "string topic
string func
int8   flag
string params
---
int32   code
string value
")

(setf (get bluesea2::ControlResponse :md5sum-) "806ff7bf5db5481c099a10480669f74f")
(setf (get bluesea2::ControlResponse :datatype-) "bluesea2/ControlResponse")
(setf (get bluesea2::ControlResponse :definition-)
      "string topic
string func
int8   flag
string params
---
int32   code
string value
")



(provide :bluesea2/Control "806ff7bf5db5481c099a10480669f74f")


