C FILE: euclidean_distance.f
      SUBROUTINE DIST_MATRIX(P, N, OUT)
C
C     CALCULATE EUCLIDEAN DISTANCE MATRIX
C     
      INTEGER N
      REAL*8 P(N,3)
      REAL*8 OUT(N,N)
Cf2py intend(in) p
Cf2py intent(in,out) out
Cf2py integer intent(hide),depend(p) :: n=shape(p,0)
C     We first abuse the last row of out to store the values of p[î]*p[i]:
      DO I=1,N
         OUT(N,I) = P(I,1)*P(I,1) + P(I,2)*P(I,2) + P(I,3)*P(I,3)
      ENDDO
C     Then we compute the upper triangle of the matrix p[i]^2 + p[j]^2 -2 (p[i]*p[j])_ij
      DO I=1,N-1
         OUT(I,I) = 0.0D0
         DO J=I+1,N
            OUT(I,J) = OUT(N,I) + OUT(N,J)
     +       - 2D0 * (P(I,1)*P(J,1) + P(I,2)*P(J,2) + P(I,3)*P(J,3))
         ENDDO
      ENDDO
C     Finally, we mirror the matrix and set OUT(N,N) = 0.
      DO I=2,N
         DO J=1,I-1
            OUT(I,J) = OUT(J,I)
         ENDDO
      ENDDO
      OUT(N,N) = 0.0D0
      END
C END FILE euclidean_distance.f
