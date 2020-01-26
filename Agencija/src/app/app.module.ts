import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { AngularFontAwesomeModule } from 'angular-font-awesome';
import { ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { OfferComponent } from './offer/offer.component';
import { ContactComponent } from './contact/contact.component';
import { HomeComponent } from './home/home.component';
import { TopOfferComponent } from './home/top-offer/top-offer.component';
import { DefaultOfferComponent } from './offer/default-offer/default-offer.component';
import { TestApiComponent } from './test-api/test-api.component';
import { LoginComponent } from './login/login.component';

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
    LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    AngularFontAwesomeModule,
    ReactiveFormsModule
  ],
  providers: [ CoreService ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
