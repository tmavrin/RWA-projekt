import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AngularFontAwesomeModule } from 'angular-font-awesome';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { OfferComponent } from './offer/offer.component';
import { ContactComponent } from './contact/contact.component';
import { HomeComponent } from './home/home.component';
import { TopOfferComponent } from './home/top-offer/top-offer.component';
import { DefaultOfferComponent } from './offer/default-offer/default-offer.component';
import { TestApiComponent } from '../core/test-api/test-api.component';
import { LoginComponent } from './login/login.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { EditOfferComponent } from './admin-panel/edit-offer/edit-offer.component';
import { AuthTokenService } from '../core/auth-token.service';

import { CoreService } from '../core/core.service';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    OfferComponent,
    ContactComponent,
    HomeComponent,
    TopOfferComponent,
    DefaultOfferComponent,
    TestApiComponent,
    LoginComponent,
    AdminPanelComponent,
    EditOfferComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    AngularFontAwesomeModule
  ],
  providers: [
    CoreService,
    { provide: HTTP_INTERCEPTORS, useClass: AuthTokenService, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
