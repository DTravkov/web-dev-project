import { HttpClient } from '@angular/common/http';
import { inject, Injectable, OnInit, signal } from '@angular/core';
import { IToken } from '../model/i-token';
import { lastValueFrom, of, retry, switchMap, tap } from 'rxjs';
import { ApiService } from './api-service';
import { Router } from '@angular/router';
import { jwtDecode } from "jwt-decode";
import { ITokenDecoded } from '../model/i-token-decoded';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private http = inject(HttpClient);
  private api = inject(ApiService);
  private router = inject(Router);

  isManager = signal<boolean>(false);

  constructor() {
    const token = this.getToken();
    if (token) this.refreshIsManager(token);
  }

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
    const token = localStorage.getItem('refresh');
    if (token) {
      this.api.postBlacklist(token)
        .pipe(retry({ count: 3, delay: 1000 })).subscribe();
    }
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    this.isManager.set(false);

    this.router.navigate(['']);
  }

  getToken(): string | null | undefined {
    return localStorage.getItem('access');
  }

  setToken(access: string, refresh: string) {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    this.refreshIsManager(access);
  }

  refreshIsManager(token: string) {
    try {
      const decoded = jwtDecode<ITokenDecoded>(token);
      const parsedDecoded = { ...decoded, user_id: Number(decoded['user_id']) };
      this.isManager.set(!!parsedDecoded.is_manager);
    } catch (e) {
      this.isManager.set(false);
    }
  }

  isLoggedIn() {
    const token = this.getToken();
    if (token) return true;
    return false;
  }


}