import { Routes } from '@angular/router';
import { DisciplineListComponent } from '../components/discipline-list-component/discipline-list-component';
import { LoginComponent } from '../components/login-component/login-component';
import { SignupComponent } from '../components/signup-component/signup-component';
import { DisciplineComponent } from '../components/discipline-component/discipline-component';

export const routes: Routes = [
    { path: '', component: DisciplineListComponent },
    { path: 'login', component: LoginComponent },
    { path: 'signup', component: SignupComponent },
    { path: 'disciplines/:id', component: DisciplineComponent },
    { path: '**', redirectTo: '' },
];
