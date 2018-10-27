//
//  TimeLine.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/26.
//  Copyright © 2018 山川拓也. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON
import AlamofireImage

class TimeLine: UIViewController, UITableViewDelegate, UITableViewDataSource{
    
    @IBOutlet weak var timeline: UITableView!
    
    let url = "https://pinky.kentaiwami.jp/promise/9"
    var pro : [Promise] = []
    
    let hoge = ["ほげ","Hello,World!","testなんやで"]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.timeline.delegate = self
        self.timeline.dataSource = self
        
        callAPI()

    }
    
    override func viewWillAppear(_ animated: Bool) {
        let titleview = UIImageView(image: UIImage(named: "pinky_header"))
        self.navigationItem.titleView = titleview
    }

    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return pro.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "TimeLineCell") as! TimeLineCell
        
        cell.profileName.text = pro[indexPath.row].name
        cell.promise.text = pro[indexPath.row].content
        cell.DateTime.text = pro[indexPath.row].created_at + "に約束しました"
        
        if pro[indexPath.row].limited_at == "" {
            cell.deliver.text = "期限なし"
        }else{
            cell.deliver.text = pro[indexPath.row].limited_at
        }

        if pro[indexPath.row].is_master {
            cell.promiseArrow.image = UIImage(named: "right")
        }else{
             cell.promiseArrow.image = UIImage(named: "left")
        }
        
        let filter = AspectScaledToFillSizeWithRoundedCornersFilter(
            size: cell.profileImg.frame.size,
            radius: 40.0
        )
        cell.profileImg.af_setImage(withURL: URL(string: pro[indexPath.row].img)!, filter: filter)
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        
        // タップ時の処理を記述
        
    }
    
    func callAPI(){
        Alamofire.request(url)
            .responseJSON{res in
                
                let json = JSON(res.value)
                let list = json["results"].arrayValue
                (0 ..< list.count).forEach { (i) in
                    var tmp = Promise(content: list[i]["content"].stringValue,
                                      created_at: list[i]["created_at"].stringValue,
                                      img: list[i]["img"].stringValue,
                                      is_master: list[i]["is_master"].boolValue,
                                      limited_at: list[i]["limited_at"].stringValue,
                                      name: list[i]["name"].stringValue
                    )
                    self.pro.append(tmp)
                }
                self.timeline.reloadData()
        }
    }
    
}
