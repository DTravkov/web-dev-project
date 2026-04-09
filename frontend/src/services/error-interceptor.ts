import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth-service';

export const authErrorInterceptor: HttpInterceptorFn = (req, next) => {
    const router = inject(Router);
    const auth = inject(AuthService);
    return next(req).pipe(
        catchError((err) => {
            if (err.status !== 401) return next(req);
            const refresh = localStorage.getItem('refresh');
            if (refresh) {
                return auth.postRefresh(refresh).pipe(
                    switchMap((response: any) => {
                        auth.setToken(response.access!, response.refresh!);
                        const newRequest = req.clone({
                            setHeaders: {
                                Authorization: `Bearer ${localStorage.getItem('access')}`
                            }
                        });

                        return next(newRequest);
                    }),
                    catchError((err) => {
                        auth.logout();
                        return throwError(() => err);
                    })
                );
            } else {
                auth.logout();
                router.navigate(['/login']);
                return throwError(() => err);
            }

        })
    )
};