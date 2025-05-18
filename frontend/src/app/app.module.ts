import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { ContactUsComponent } from './components/contact-us/contact-us.component';
import { ModelComponent } from './components/model/model.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import { NavComponent } from './components/nav/nav.component';
import { TakeTestComponent } from './components/take-test/take-test.component';
import {AuthInterceptor} from "./interceptor/auth.interceptor";
import { DragDropDirective } from './directives/drag-drop.directive';
import { FileSizePipe } from './pipe/file-size.pipe';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    DashboardComponent,
    ContactUsComponent,
    ModelComponent,
    NavComponent,
    TakeTestComponent,
    DragDropDirective,
    FileSizePipe
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        HttpClientModule,
        ReactiveFormsModule
    ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
