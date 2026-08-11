import { Routes } from '@angular/router';
import { CasesList } from './cases-list/cases-list';
import { CaseForm } from './case-form/case-form';

export const routes: Routes = [
  { path: '', component: CasesList },
  { path: 'cases/new', component: CaseForm },
];