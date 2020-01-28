import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ContactComponent } from './contact/contact.component';
import { OfferComponent } from './offer/offer.component';
import { LoginComponent } from './login/login.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { TestApiComponent } from '../core/test-api/test-api.component';

import { AuthGuard } from '../core/auth.guard';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'offer', component: OfferComponent },
  { path: 'login', component: LoginComponent},
  { path: 'admin', component: AdminPanelComponent/*, canActivate: [ AuthGuard ]*/},
  { path: 'test-api', component: TestApiComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
