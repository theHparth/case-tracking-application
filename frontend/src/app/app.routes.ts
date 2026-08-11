import { Routes } from '@angular/router';
import { CasesList } from './cases-list/cases-list';
import { CaseForm } from './case-form/case-form';
import { Login } from './login/login';

export const routes: Routes = [
  { path: '', component: CasesList },
  { path: 'login', component: Login },
  { path: 'cases/new', component: CaseForm },
];