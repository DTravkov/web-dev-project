import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { IToken } from '../model/i-token';
import { tap } from 'rxjs';
import { ApiService } from './api-service';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private api = inject(ApiService);

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
    localStorage.removeItem('refresh');
  }


  // ! may be wrong with types here
  getToken(): string | null | undefined {
    return localStorage.getItem('access');

  }

  setToken(access: string, refresh: string) {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
  }

  isLoggedIn() {
    const token = this.getToken();
    if (token) return true;
    return false;
  }

}
