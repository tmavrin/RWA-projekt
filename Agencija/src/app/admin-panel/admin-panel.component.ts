import { Component, OnInit } from '@angular/core';
import { CoreService } from '../../core/core.service';

@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.scss']
})
export class AdminPanelComponent implements OnInit {

  offers: any;
  pageNo = 0;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.getOffers();
  }

  getOffers() {
    this.coreService.getOffersByPage(this.pageNo, 15).subscribe(
      data => { this.offers = data; },
      error => { console.log(error.message); }
    );
  }
}
