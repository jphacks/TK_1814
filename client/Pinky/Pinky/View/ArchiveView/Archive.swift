//
//  TimeLine.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/26.
//  Copyright © 2018 山川拓也. All rights reserved.
//

import UIKit
import Alamofire
import AlamofireImage
import SwiftyJSON

class Archive: UIViewController, UICollectionViewDataSource, UICollectionViewDelegate {
    
    @IBOutlet weak var archs: UICollectionView!
    
    let url = "https://pinky.kentaiwami.jp/archive/9"
    var arch : [Archives] = []
   
    private weak var refreshControl: UIRefreshControl!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        initializePullToRefresh()
        
        callAPI()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        let titleview = UIImageView(image: UIImage(named: "pinky_header"))
        self.navigationItem.titleView = titleview
        refresh()
    }
    
    func collectionView(_ collectionView: UICollectionView,
                        cellForItemAt indexPath: IndexPath) -> UICollectionViewCell{
        
        let testCell:UICollectionViewCell =
            collectionView.dequeueReusableCell(withReuseIdentifier: "Cell",
                                               for: indexPath)
        
        let imageView = testCell.contentView.viewWithTag(1) as! UIImageView
        let filter = AspectScaledToFillSizeWithRoundedCornersFilter(
            size: imageView.frame.size,
            radius: 0.0
        )
        imageView.af_setImage(withURL: URL(string: arch[indexPath.row].img)!, filter: filter)
        
        let label = testCell.contentView.viewWithTag(2) as! UILabel
        label.text = arch[indexPath.row].name
        
        let label2 = testCell.contentView.viewWithTag(3) as! UILabel
        label2.text = String(arch[indexPath.row].count)
        
        return testCell
    }
    
    func numberOfSections(in collectionView: UICollectionView) -> Int {
        return 1
    }
    
    func collectionView(_ collectionView: UICollectionView,
                        numberOfItemsInSection section: Int) -> Int {
        return self.arch.count
    }
    
    func collectionView(_ collectionView: UICollectionView,
                        layout collectionViewLayout: UICollectionViewLayout,
                        sizeForItemAt indexPath: IndexPath) -> CGSize {
        
        let horizontalSpace:CGFloat = 2
        let cellSize:CGFloat = self.view.bounds.width/2 - horizontalSpace

        return CGSize(width: cellSize, height: cellSize)
    }
    
    func callAPI(){
        Alamofire.request(url)
            .responseJSON{res in
                
                let json = JSON(res.value)
                
                let list = json["results"].arrayValue
                print(list)
                (0 ..< list.count).forEach { (i) in
                    var tmp = Archives(count: list[i]["count"].intValue,
                                       name: list[i]["name"].stringValue,
                                      img: list[i]["img"].stringValue,
                                      user_id: list[i]["content"].intValue
                    )
                    self.arch.append(tmp)
                }
                self.archs.reloadData()
        }
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    /********************* Pull to refresh関連 *********************/
    private func initializePullToRefresh() {
        let control = UIRefreshControl()
        control.addTarget(self, action: #selector(onPullToRefresh(_:)), for: .valueChanged)
        archs.addSubview(control)
        refreshControl = control
    }
    
    @objc private func onPullToRefresh(_ sender: AnyObject) {
        refresh()
        
    }
    
    private func stopPullToRefresh() {
        if refreshControl.isRefreshing {
            refreshControl.endRefreshing()
        }
    }
    
    private func refresh() {
        DispatchQueue.global().async {
            Thread.sleep(forTimeInterval: 1.0)
            DispatchQueue.main.async {
                self.completeRefresh()
            }
        }
    }
    
    private func completeRefresh() {
        stopPullToRefresh()
        self.arch.removeAll()
        callAPI()
        archs.reloadData()
        //        let calender = Calender()
        //        calender.addEvent(limited_at: <#T##String#>, title: <#T##String#>, endDate: <#T##String#>)
    }
    /********************************************************/
}

