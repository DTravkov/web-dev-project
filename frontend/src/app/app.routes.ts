import { Routes } from '@angular/router';
import { DisciplineListPage } from '../pages/discipline-list-page/discipline-list-page';
import { DisciplinePage } from '../pages/discipline-page/discipline-page';
import { OfferPage } from '../pages/offer-page/offer-page';
import { ApproveListPage } from '../pages/approve-list-page/approve-list-page';
import { ProfilePage } from '../pages/profile-page/profile-page';
import { ProfessorListPage } from '../pages/professor-list-page/professor-list-page';
import { ProfessorPage } from '../pages/professor-page/professor-page';

export const routes: Routes = [
    { path: 'disciplines', component: DisciplineListPage },
    { path: 'disciplines/users/:id', component: ProfilePage },
    { path: 'disciplines/approve-list', component: ApproveListPage },
    { path: 'disciplines/offer', component: OfferPage },
    { path: 'disciplines/:id', component: DisciplinePage },
    { path: 'professors', component: ProfessorListPage },
    { path: 'professors/:id', component: ProfessorPage },
    { path: '**', redirectTo: 'disciplines' },
];
