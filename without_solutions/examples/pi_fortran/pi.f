      SUBROUTINE APPROX_PI(N_ATTEMPTS, OUT)
C
C     MONTE CARLO COMPUTATION TO APPROXIMATE PI
C     
      INTEGER N_ATTEMPTS
      REAL*8 OUT
      REAL*8 X, Y
Cf2py intend(in) n_attempts
Cf2py intent(out) out
      INTEGER N_HITS

      N_HITS = 0
      
      CALL SRAND(86456)

      DO I=1,N_ATTEMPTS
         X = 2.0D0 * RAND() - 1.0D0
         Y = 2.0D0 * RAND() - 1.0D0
         IF (X*X + Y*Y <= 1.0D0) THEN
            N_HITS = N_HITS + 1
         ENDIF
      ENDDO
      OUT = 4.0D0 * N_HITS / N_ATTEMPTS
      END
