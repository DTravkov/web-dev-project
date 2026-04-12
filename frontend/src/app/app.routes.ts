import { Routes } from '@angular/router';
import { DisciplineListPage } from '../pages/discipline-list-page/discipline-list-page';
import { LoginComponent } from '../components/login-component/login-component';
import { SignupComponent } from '../components/signup-component/signup-component';
import { DisciplinePage } from '../pages/discipline-page/discipline-page';
import { OfferPage } from '../pages/offer-page/offer-page';
import { ApproveListPage } from '../pages/approve-list-page/approve-list-page';

export const routes: Routes = [
    { path: 'disciplines', component: DisciplineListPage },
    { path: 'login', component: LoginComponent },
    { path: 'signup', component: SignupComponent },
    { path: 'disciplines/approve-list', component: ApproveListPage },
    { path: 'disciplines/offer', component: OfferPage },
    { path: 'disciplines/:id', component: DisciplinePage },
    { path: '**', redirectTo: 'disciplines' },
];
