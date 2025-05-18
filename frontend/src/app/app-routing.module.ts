import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {RegisterComponent} from "./components/register/register.component";
import {DashboardComponent} from "./components/dashboard/dashboard.component";
import {ContactUsComponent} from "./components/contact-us/contact-us.component";
import {ModelComponent} from "./components/model/model.component";
import {AuthGuard} from "./guards/auth.guard";
import {AdminGuard} from "./guards/admin.guard";
import {TakeTestComponent} from "./components/take-test/take-test.component";

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'contact-us',
    component: ContactUsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "take-test",
    component: TakeTestComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'model',
    component: ModelComponent,
    canActivate: [AuthGuard, AdminGuard],
  },
  { path: '**', redirectTo: 'login' },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
