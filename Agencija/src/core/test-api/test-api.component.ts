import { Component, OnInit } from '@angular/core';
import { Offer } from '../VO/Offer';
import { CoreService } from '../core.service';
import { User } from '../VO/User';

@Component({
  selector: 'app-test-api',
  templateUrl: './test-api.component.html',
  styleUrls: ['./test-api.component.scss']
})
export class TestApiComponent implements OnInit {

  results: any;

  constructor(protected coreService: CoreService) { }

  ngOnInit() {
    this.results = 'start';
  }

  login() {
    const u = new User('patkica', 'mala');
    this.coreService.login(u).subscribe(data => {
      this.results = data;
      console.log(this.results);
    }, error => { this.results = error.message; });
  }

  register() {
    const u = new User('patkica', 'mala');
    this.coreService.register(u).subscribe(data => {
      this.results = data;
      console.log(this.results);
    }, error => { this.results = error.message; });
  }

  getOffers() {
    this.coreService.getOffersByPage(2).subscribe( data => {
      this.results = data;
      console.log(this.results);
    }, error => { this.results = error.message; });
  }

  addOffer() {
    const o = new Offer(
      'Nature Tour',
      'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla,' +
      'nullam tellus feugiat aptent torquent nec. Eu velit ridiculus lacinia dignissim viverra magnis dapibus congue praesent.',
      1800);
    this.coreService.addOffer(o).subscribe(data => {}, error => { this.results = error.message; });
  }

  editOffer() {
    this.coreService.getOffersByPage(3).subscribe( data => {
      const o = data[0];
      o.description = 'YAS QUEEN';
      this.coreService.editOffer(o).subscribe(data2 => {}, error => { this.results = error.message; });
    }, error => { this.results = error.message; });
  }

  deleteOffer() {
    this.coreService.deleteOffer('5f1a95f5-404b-11ea-ba57-0242ac110004').subscribe(data => {}, error => { this.results = error.message; });
  }

  getTopOffers() {
    this.coreService.getTopList().subscribe( data => {
      this.results = data;
      console.log(this.results);
    }, error => { this.results = error.message; });
  }

}
