//
//  TimeLineCell.swift
//  Pinky
//
//  Created by 山川拓也 on 2018/10/27.
//  Copyright © 2018 山川拓也. All rights reserved.
//

import UIKit

class TimeLineCell: UITableViewCell {
    @IBOutlet var profileImg: UIImageView!
    @IBOutlet var promiseArrow: UIImageView!
    @IBOutlet var clockImg: UIImageView!
    @IBOutlet var deliver: UILabel!
    @IBOutlet var profileName: UILabel!
    @IBOutlet var DateTime: UILabel!
    @IBOutlet var promise: UILabel!
    @IBOutlet weak var compLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
