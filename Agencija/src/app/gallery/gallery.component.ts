import { Component, OnInit } from '@angular/core';
import { CoreService } from 'src/core/core.service';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.scss']
})
export class GalleryComponent implements OnInit {
  protected imageList: [];
  public backendUrl = 'http://178.238.232.172:8080';

  constructor(private coreService: CoreService) {}

  ngOnInit() {
    this.coreService.getGallery().subscribe(
      (data: []) => {
        this.imageList = data;
        data.pop();
      },
      error => {
        console.error(error);
      }
    );
  }
}
