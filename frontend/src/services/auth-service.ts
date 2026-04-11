import { HttpClient } from '@angular/common/http';
import { inject, Injectable, OnInit, signal } from '@angular/core';
import { IToken } from '../model/i-token';
import { lastValueFrom, switchMap, tap } from 'rxjs';
import { ApiService } from './api-service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private api = inject(ApiService);
  private router = inject(Router);


  postLogin(username: string, password: string) {
    return this.http.post<IToken>('http://127.0.0.1:80/api/token/', { username: username, password: password }, { headers: { "Content-Type": "application/json" } })
      .pipe(
        tap((response) => {
          this.setToken(response.access!, response.refresh!);
        })
      );
  }

  postSignup(username: string, password: string) {
    return this.http.post('http://127.0.0.1:80/api/signup/', { "username": username, "password": password }, { headers: { "Content-Type": "application/json" } });
  }

  postRefresh(refresh: string) {
    return this.http.post<IToken>('http://127.0.0.1:80/api/token/refresh/', { "refresh": refresh }, { headers: { "Content-Type": "application/json" } })
      .pipe(
        tap((response) => {
          this.setToken(response.access!, response.refresh!);
        })
      );
  }


  logout() {
    localStorage.removeItem('access');
    if (localStorage.getItem('refresh')) this.api.postBlacklist(localStorage.getItem('refresh')!).subscribe();
    localStorage.removeItem('refresh');
    this.deleteIsModerator();
    this.router.navigate(['']);
  }


  getToken(): string | null | undefined {
    return localStorage.getItem('access');

  }

  setToken(access: string, refresh: string) {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    this.deleteIsModerator();
  }

  isModerator() {
    const isModer = localStorage.getItem('ismoderator');
    if (!isModer) this.api.getIsModerator().subscribe(
      {
        next(value) { localStorage.setItem('ismoderator', "yes") },
        error(err) { localStorage.setItem('ismoderator', "no") },
      }
    );
    return isModer === "yes"
  }

  deleteIsModerator() {
    localStorage.removeItem('ismoderator');
  }

  isLoggedIn() {
    const token = this.getToken();
    if (token) return true;
    return false;
  }


}
