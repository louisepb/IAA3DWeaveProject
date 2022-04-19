      SUBROUTINE MPC(UE,A,JDOF,MDOF,N,JTYPE,X,U,UINIT,MAXDOF,
     * LMPC,KSTEP,KINC,TIME,NT,NF,TEMP,FIELD,LTRAN,TRAN)
      INCLUDE 'ABA_PARAM.INC'
      DIMENSION A(N),JDOF(N),X(6,N),U(MAXDOF,N),UINIT(MAXDOF,N),
     * TIME(2),TEMP(NT,N),FIELD(NF,NT,N),LTRAN(N),TRAN(3,3,N)
      AA=X(1,1)-X(1,2)
	  BB=X(2,1)-X(2,2)
	  CC=X(3,1)-X(3,2)
	  XX=(X(1,1)+X(1,2))/2.
      YY=(X(2,1)+X(2,2))/2.
      ZZ=(X(3,1)+X(3,2))/2.
	  A(1)=1.
      A(2)=-1.
      JDOF(1:N)=1
! *** X-Faces
      IF(JTYPE.EQ.1) THEN
        A(3)=-AA
        A(4)=-AA*ZZ
      ELSEIF(JTYPE.EQ.2) THEN
        JDOF(1)=2
        JDOF(2)=2
        A(3)=-AA*ZZ/2.
      ELSEIF(JTYPE.EQ.3) THEN
        JDOF(1)=3
        JDOF(2)=3
        A(3)=AA*XX
        A(4)=AA*YY/2.
! *** Y-Faces
      ELSEIF(JTYPE.EQ.4) THEN
        A(3)=-BB
        A(4)=-BB*ZZ/2.
      ELSEIF(JTYPE.EQ.5) THEN
        JDOF(1)=2
        JDOF(2)=2
        A(3)=-BB
        A(4)=-BB*ZZ
      ELSEIF(JTYPE.EQ.6) THEN
        JDOF(1)=3
        JDOF(2)=3
        A(3)=BB*YY
        A(4)=BB*XX/2.
! *** Edges
      ELSEIF(JTYPE.EQ.7) THEN
        A(3)=-AA
        A(4)=-AA*ZZ
        A(5)=-BB
        A(6)=-BB*ZZ/2.
      ELSEIF(JTYPE.EQ.8) THEN
        JDOF(1)=2
        JDOF(2)=2
        A(3)=-AA*ZZ/2.
        A(4)=-BB
        A(5)=-BB*ZZ
      ELSEIF(JTYPE.EQ.9) THEN
        JDOF(1)=3
        JDOF(2)=3
        A(3)=AA*XX/2.
        A(4)=BB*YY/2.
        A(5)=(AA*YY+BB*XX)/2.
      ENDIF
      RETURN
      END
