import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AngularFontAwesomeModule } from 'angular-font-awesome';

import { AppComponent } from './app.component';
import { NavbarUserComponent } from './navbar/navbar-user/navbar-user.component';
import { NavbarAdminComponent } from './navbar/navbar-admin/navbar-admin.component';
import { OfferComponent } from './offer/offer.component';
import { ContactComponent } from './contact/contact.component';
import { HomeComponent } from './home/home.component';
import { TopOfferComponent } from './home/top-offer/top-offer.component';
import { DefaultOfferComponent } from './offer/default-offer/default-offer.component';
import { TestApiComponent } from '../core/test-api/test-api.component';
import { LoginComponent } from './login/login.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { EditOfferComponent } from './admin-panel/edit-offer/edit-offer.component';
import { PaginationComponent } from './pagination/pagination.component';

import { CoreService } from '../core/core.service';
import { AuthTokenService } from '../core/auth-token.service';
import { GalleryComponent } from './gallery/gallery.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarUserComponent,
    NavbarAdminComponent,
    OfferComponent,
    ContactComponent,
    HomeComponent,
    TopOfferComponent,
    DefaultOfferComponent,
    TestApiComponent,
    LoginComponent,
    AdminPanelComponent,
    EditOfferComponent,
    PaginationComponent,
    GalleryComponent
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
