
(cl:in-package :asdf)

(defsystem "bluesea2-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Control" :depends-on ("_package_Control"))
    (:file "_package_Control" :depends-on ("_package"))
    (:file "DefenceZone" :depends-on ("_package_DefenceZone"))
    (:file "_package_DefenceZone" :depends-on ("_package"))
  ))